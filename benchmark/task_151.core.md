
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--(^)

# poly_type
Ad-hoc

# signature
```haskell
(^) :: (Num a, Integral b) => a -> b -> a
```   

# code
```haskell
x ^ y | y < 0 = error "negative"
      | y == 0 = 1
      | otherwise = powImpl x y
```

# dependencies
## 0
```haskell
(<), (==) :: Ord a => a -> a -> Bool
```
## 1
```haskell
powImpl :: (Num a, Integral b) => a -> b -> a
```