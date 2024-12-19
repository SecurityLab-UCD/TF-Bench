
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Either.hs--either

# poly_type
Parametric

# signature
```haskell
f1 :: (a -> c) -> (b -> c) -> A a b -> c
```   

# code
```haskell
f1 _ g (B y)    =  g y
f1 f _ (C x)     =  f x
```

# dependencies

## 0
```haskell
data A a b = B a | C b
```
## 1
```haskell
B :: a -> A a b
```
## 2
```haskell
C :: b -> A a b
```