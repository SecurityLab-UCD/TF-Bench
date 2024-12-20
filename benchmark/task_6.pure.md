
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
f1 = f2 . (+ 1) . f3
```

# dependencies
## 0
```haskell
f2 :: T1 a => T2 -> a
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
(+) :: T2 -> T2 -> T2
```
## 3
```haskell
f3 :: T1 a => a -> T2
```