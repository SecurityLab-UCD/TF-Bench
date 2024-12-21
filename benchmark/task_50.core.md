
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--mconcat

# poly_type
Ad-hoc

# signature
```haskell
mconcat :: Monoid a => [a] -> a
```   

# code
```haskell
mconcat = foldr mappend mempty
```

# dependencies
## 0
```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
```
## 1
```haskell
mappend :: Monoid a => a -> a -> a
```
## 2
```haskell
mempty :: Monoid a => a
```
