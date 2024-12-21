
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--isNaN-Float

# poly_type
Monomorphic

# signature
```haskell
isNaN :: Float -> Bool
```   

# code
```haskell
isNaN x = 0 /= isFloatNaN x
```

# dependencies
## 0
```haskell
isFloatNaN :: Float -> Int
```
## 1
```haskell
(/=) :: Int -> Int -> Bool
```