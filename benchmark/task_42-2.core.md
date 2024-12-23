
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--isInfinite-Double

# poly_type
Monomorphic

# signature
```haskell
isInfinite :: Double -> Bool
```   

# code
```haskell
isInfinite x        = 0 /= isDoubleInfinite x
```

# dependencies
## 0
```haskell
isDoubleInfinite :: Double -> Int
```
##
```haskell
(/=) :: Int -> Int -> Bool
```
