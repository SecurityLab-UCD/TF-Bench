
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
floatRange x =  (dbl_min_exp, dbl_max_exp)
```

# dependencies
## 0
```haskell
dbl_min_exp :: Int
```
## 1
```haskell
dbl_min_exp :: Int
```
## 2
```haskell
x :: Float
```
