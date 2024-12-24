
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--floatRange-Float

# poly_type
Monomorphic

# signature
```haskell
floatRange :: Float -> (Int,Int)
```   

# code
```haskell
floatRange x =  (DBL_MIN_EXP, DBL_MAX_EXP)
```

# dependencies
## 0
```haskell
DBL_MIN_EXP :: Int
```
## 1
```haskell
DBL_MAX_EXP :: Int
```
## 2
```haskell
x :: Float
```
