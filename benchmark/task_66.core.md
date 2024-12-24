
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Traversable.hs--sequenceA

# poly_type
Ad-hoc

# signature
```haskell
sequenceA :: (Traversable t, Applicative f) => t (f a) -> f (t a)
```   

# code
```haskell
sequenceA = traverse id
```

# dependencies
## 0
```haskell
traverse :: (Traversable t, Applicative f) => (a -> f b) -> t a -> f (t b)
```
## 1
```haskell
id :: a -> a
```
