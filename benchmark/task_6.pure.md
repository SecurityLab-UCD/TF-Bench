
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ

# poly_type
Ad-hoc

# note
modified

# signature
```haskell
f1 :: T1 a => a -> a
```  

# code
```haskell
f1 (c :: T2) =  f2 (f3 c + 1)
f1 T5 = T6
f1 (x :: T3) = x + 1
```

# dependencies
## 0
```haskell
class T1 a = {T2, T3, T4}
```
## 1
```haskell
f2 :: T3 -> T2
```
## 2
```haskell
f3 :: T2 -> T3
```
## 3
```haskell
(+) :: T3 -> T3 -> T3
```
## 4
```haskell
data T4 = T5 | T6
```