
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
f1 T6 = T7
f1 T7  = error "bad argument"
f1 T8 = T9
f1 T9 = T10
f1 T10 = error "bad argument"
f1 c =  f2 (f3 c + 1)
f1 x = x + 1
```

# dependencies
## 0
```haskell
class T1 a = {T2, T3, T4, T5}
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
data T4 = T6 | T7
```
## 5
```haskell
data T5 = T8 | T9 | T10
```