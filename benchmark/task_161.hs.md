
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(*>)

# poly_type
Ad-hoc 

# signature
```haskell
(*>) :: Applicative f => f a -> f b -> f b
```   

# code
```haskell
a1 *> a2 = (id <$ a1) <*> a2
```

# dependencies
## 0
```haskell
id :: a -> a
```
## 1
```haskell
(<$) :: Functor f => a -> f b -> f a
```
## 2
```haskell
(<*>) :: Applicative f => f (a -> b) -> f a -> f b
```
