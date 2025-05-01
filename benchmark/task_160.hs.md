
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(<*)

# poly_type
Ad-hoc 

# signature
```haskell
(<*) :: Applicative f => f a -> f b -> f a
```   

# code
```haskell
(<*) = liftA2 const
```

# dependencies
## 0
```haskell
liftA2 :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
```
## 1
```haskell
const :: a -> b -> a
```
