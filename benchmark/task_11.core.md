
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--enumFromThen

# poly_type
Parametric

# signature
```haskell
enumFromThen :: Enum a => a -> a -> [a]
```   

# code
```haskell
enumFromThen x y = map toEnum [fromEnum x, fromEnum y ..]
```

# dependencies
## 0
```haskell
map :: (a -> b) -> [a] -> [b]
```
## 1
```haskell
toEnum :: Enum a => Int -> a
```
## 2
```haskell
fromEnum :: Enum => a -> Int
```