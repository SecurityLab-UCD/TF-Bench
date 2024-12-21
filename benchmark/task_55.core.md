
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--mapM_

# poly_type
Ad-hoc

# signature
```haskell
mapM_ :: (Foldable t, Monad m) => (a -> m b) -> t a -> m ()
```   

# code
```haskell
mapM_ f = foldr c (return ())
  where c x k = f x >> k
```

# dependencies
## 0
```haskell
(>>) :: forall a b. m a -> m b -> m b
```
## 1
```haskell
foldr :: (a -> b -> b) -> b -> t a -> b
```
## 2
```haskell
return :: a -> m a
```
