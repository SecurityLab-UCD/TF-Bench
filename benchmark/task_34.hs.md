
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
floatDigits x = dbl_mant_dig
```
# dependencies
## 0
```haskell
dbl_mant_dig :: Int
```
## 1
```haskell
x :: Float
```
