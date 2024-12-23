
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(<*>)

# poly_type
Ad-hoc 

# signature
```haskell
(<*>) :: Applicative f => f (a -> b) -> f a -> f b 
```   

# code
```haskell
(<*>) = liftA2 id
```

# dependencies
## 0
```haskell
id :: a -> a
```
## 1
```haskell
liftA2 :: Apply f => (a -> b -> c) -> f a -> f b -> f c
```
