
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe

# poly_type
Parametric

# signature
```haskell
f1 :: b -> (a -> b) -> T1 a -> b
```   

# code
```haskell
f1 _ f (T2 x) = f x
f1 n _ T3  = n
```

# dependencies
## 0
```haskell
data T1 a = T3 | T2 a
```
## 1
```haskell
T2 :: a -> T1 a
```
## 2
```haskell
T3 :: T1 a
```
