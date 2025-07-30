import asyncio
from abc import ABC, abstractmethod

from webtool.cache.client import RedisCache
from webtool.throttle.decorator import LimitRule
from webtool.utils.json import ORJSONDecoder, ORJSONEncoder


class BaseLimiter(ABC):
    @abstractmethod
    def is_deny(self, identifier: str, rules: list[LimitRule]) -> list[float]:
        """
        Checks if any rate limits are exceeded.

        Parameters:
            identifier: User or session identifier
            rules: List of rate limit rules to check

        Returns:
            list[float]: List of waiting times until rate limits reset (empty if not exceeded)
        """

        raise NotImplementedError


class RedisLimiter(BaseLimiter):
    """
    Rate limiter implementation using Redis for distributed rate limiting.
    """

    _LUA_LIMITER_SCRIPT = """
    -- Retrieve arguments
    -- ruleset = {key: [limit, window_size], ...}
    -- return = {key: [limit, current, exist first request], ...}
    local now = tonumber(ARGV[1])
    local ruleset = cjson.decode(ARGV[2])

    for i, key in ipairs(KEYS) do
        -- Step 1: Remove expired requests from the sorted set
        redis.call('ZREMRANGEBYSCORE', key, 0, now - ruleset[key][2])

        -- Step 2: Count the number of requests within the valid time window
        local amount = redis.call('ZCARD', key)

        -- Step 3: Add the current request timestamp to the sorted set
        if amount <= ruleset[key][1] then
            redis.call('ZADD', key, now, tostring(now))
            amount = amount + 1
        end

        -- Step 4: Set the TTL for the key
        redis.call("EXPIRE", key, ruleset[key][2])
        ruleset[key][2] = amount
        ruleset[key][3] = redis.call("ZREVRANGE", key, 0, 0)[1]
    end

    return cjson.encode(ruleset)
    """

    def __init__(self, redis_cache: RedisCache):
        """
        Parameters:
             redis_cache: Redis client instance
        """

        self._cache = redis_cache.cache
        self._redis_function = self._cache.register_script(RedisLimiter._LUA_LIMITER_SCRIPT)
        self._json_encoder = ORJSONEncoder()
        self._json_decoder = ORJSONDecoder()

    @staticmethod
    def _get_ruleset(identifier: str, rules: list[LimitRule]) -> dict[str, tuple[int, int]]:
        """
        Constructs a ruleset dictionary mapping keys to limits and intervals.

        Parameters:
            identifier: User or session identifier
            rules: List of rate limit rules to apply

        Returns:
            dict[str, tuple[int, int]]: Dictionary of {key: (max_requests, interval)}
        """

        ruleset = {identifier + rule.throttle_key: (rule.max_requests, rule.interval) for rule in rules}

        return ruleset

    async def _get_limits(self, ruleset) -> dict[str, list[int, int]]:
        """
        Executes the rate limiting Lua script in Redis.

        Parameters:
            ruleset: Dictionary of rate limit rules

        Returns:
            dict[str, list[int, int]]: Dictionary of updated counts and timestamps
        """

        now = asyncio.get_running_loop().time()

        result = await self._redis_function(keys=list(ruleset.keys()), args=[now, self._json_encoder.encode(ruleset)])
        result = self._json_decoder.decode(result)

        return result

    async def is_deny(self, identifier: str, rules: list[LimitRule]) -> list[tuple[int, int, float]]:
        """
        Checks if any rate limits are exceeded.

        Parameters:
            identifier: User or session identifier
            rules: List of rate limit rules to check

        Returns:
            list[int, int, float]: List of (Limit Amount, Current, Time until rate limit reset (in seconds))
        """

        ruleset = self._get_ruleset(identifier, rules)  # ruleset = {key: [limit, window_size], ...}
        result = await self._get_limits(ruleset)  # {key: [limit, amount, exist first request], ...}

        now = asyncio.get_running_loop().time()
        deny = [(val[0], val[1], float(val[2]) + ruleset[key][1] - now) for key, val in result.items()]

        return deny
