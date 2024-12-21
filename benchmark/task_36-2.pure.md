
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Double

# poly_type
Parametric

# signature
```haskell
f1 :: T1 -> (T2, T3)
```   

# code
```haskell
f1 (f2 x#) = case f3 x#   of
                      (# i, j #) -> (i, f4 j)
```

# dependencies
## 0
```haskell
f2 :: T4 -> T1
```
## 1
```haskell
f3 :: T4 -> (# T2, T5 #)
```
## 2
```haskell
f4 :: T5 -> T3
```