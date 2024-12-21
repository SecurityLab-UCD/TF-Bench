
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Float

# poly_type
Parametric

# signature
```haskell
f1 :: T1 -> (T2, T3)
```   

# code
```haskell
f1 (f5 f#) = case f2# f# of
                      (# i, e #) -> (f3 i, f4 e)
```

# dependencies
## 0
```haskell
f5 :: T4 -> T1
```
## 1
```haskell
f2# :: T4 -> (# T5, T5 #)
```
## 2
```haskell
f3 :: T5 -> T2
```
## 3
```haskell
f4 :: T5 -> T3
```