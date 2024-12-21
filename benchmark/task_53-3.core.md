
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--liftA2--(,)

# poly_type
Parametric

# signature
```haskell
liftA2 :: (a0 -> b -> c) -> (a, a0) -> (a, b) -> (a, c)
```   

# code
```haskell
liftA2 f (u, x) (v, y) = (u <> v, f x y)
```

# dependencies
## 0
```haskell
(<>) :: a -> a -> a
```
