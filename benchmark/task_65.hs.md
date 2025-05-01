
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Traversable.hs--traverse

# poly_type
Ad-hoc

# signature
```haskell
traverse :: (Traversable t, Applicative f) => (a -> f b) -> t a -> f (t b)
```   

# code
```haskell
traverse f = sequenceA . fmap f
```

# dependencies
## 0
```haskell
sequenceA :: (Traversable t, Applicative f) => t (f a) -> f (t a)
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
fmap :: Functor f => (a -> b) -> f a -> f b
```
