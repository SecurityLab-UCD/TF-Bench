
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--encodeFloat-Double

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T2 -> T3
```   

# code
```haskell
f1 i (f2 j) = f3 (f4 i j)
```

# dependencies
## 0
```haskell
f2 :: T4 -> T2
```
## 1
```haskell
f3 :: T5 -> T3
```
## 2
```haskell
f4 :: T1 -> T4 -> T5
```