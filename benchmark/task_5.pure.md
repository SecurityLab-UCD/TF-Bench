
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Tuple.hs--uncurry

# poly_type
Parametric

# signature
```haskell
f1 :: (a -> b -> c) -> ((a, b) -> c)
```   

# code
```haskell
f1 f p             =  f (f2 p) (f3 p)
```

# dependencies
## 0
```haskell
f2 :: (a,b) -> a
```
## 1
```haskell
f3 :: (a,b) -> b
```
