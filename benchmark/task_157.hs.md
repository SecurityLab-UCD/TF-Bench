
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(<$)

# poly_type
Ad-hoc

# signature
```haskell
(<$) :: Functor f => a -> f b -> f a
```   

# code
```haskell
(<$) = fmap . const
```

# dependencies
## 0
```haskell
fmap :: Functor f => (a -> b) -> f a -> f b
```
## 1
```haskell
const :: a -> b -> a
```
## 3
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
