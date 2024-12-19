
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Tuple.hs--uncurry

# poly_type
Parametric

# signature
```haskell
uncurry :: (a -> b -> c) -> ((a, b) -> c)
```   

# code
```haskell
uncurry f p             =  f (fst p) (snd p)
```

# dependencies
## 0
```haskell
snd :: (a,b) -> b
```
## 1
```haskell
fst :: (a,b) -> a
```
