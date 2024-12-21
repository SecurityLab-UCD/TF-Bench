
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--liftA2

# poly_type
Ad-hoc

# signature
```haskell
liftA2 :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
```   

# code
```haskell
liftA2 f x = (<*>) (fmap f x)
```

# dependencies
## 0
```haskell
(<*>) :: f (a -> b) -> f a -> f b
```
## 1
```haskell
fmap :: (a -> b) -> f a -> f b
```

