local function add(a, b)
    return a + b
end

local function subtract(a, b)
    return a - b
end

local function multiply(a, b)
    return a * b
end

local function main()
    local result = 10
    result = add(result, 5)
    result = multiply(result, 2)
    result = subtract(result, 4)
    assert(result == 34, "Math operations failed")
    return result
end

return main()
