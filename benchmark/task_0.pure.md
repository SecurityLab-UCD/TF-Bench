
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe

# poly_type
Parametric

# signature
```haskell
f :: b -> (a -> b) -> A a -> b
```   

# code
```haskell
maybe _ f (B x) = f x
maybe n _ C  = n
```

# dependencies
## 0
```haskell
data A a = C | B a
```
## 1
```haskell
B :: a -> A a
```
## 2
```haskell
C :: A a
```
