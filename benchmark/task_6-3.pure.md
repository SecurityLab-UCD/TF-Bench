
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ-Char

# poly_type
Monomorphic

# note
modified

# signature
```haskell
f1 :: T1 -> T1
```  

# code
```haskell
f1 c =  f2 (f3 c + 1)
```

# dependencies
## 0
```haskell
f2 :: T2 -> T1
```
## 1
```haskell
f3 :: T1 -> T2
```
## 2
```haskell
(+) :: T2 -> T2 -> T2
```