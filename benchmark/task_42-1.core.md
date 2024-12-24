
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--isInfinite-Float

# poly_type
Monomorphic

# signature
```haskell
isInfinite :: Float -> Bool
```   

# code
```haskell
isInfinite x = 0 /= isFloatInfinite x
```

# dependencies
## 0
```haskell
isFloatInfinite :: Float -> Int
```
## 1
```haskell
(/=) :: Int -> Int -> Bool
```