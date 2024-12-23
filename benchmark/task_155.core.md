
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--mempty

# poly_type
Ad-hoc

# signature
```haskell
mempty :: Monoid a => a
```   

# code
```haskell
mempty = mconcat []
```

# dependencies
## 0
```haskell
mconcat :: Monoid a => [a] -> a
```
