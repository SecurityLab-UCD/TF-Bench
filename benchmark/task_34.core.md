
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--floatDigits-Float

# poly_type
Monomorphic

# signature
```haskell
floatDigits :: Float -> Int
```   

# code
```haskell
floatDigits x = DBL_MANT_DIG
```
# dependencies
## 0
```haskell
DBL_MANT_DIG :: Int
```
## 1
```haskell
x :: Float
```
