
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--liftA2--[]

# poly_type
Parametric

# signature
```haskell
liftA2 :: (a -> b -> c) -> [a] -> [b] -> [c]
```   

# code
```haskell
liftA2 f xs ys = [f x y | x <- xs, y <- ys]
```

# dependencies
