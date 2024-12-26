
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldl

# poly_type
Parametric

# signature
```haskell
foldl :: (b -> a -> b) -> b -> t a -> b
```   

# code
```haskell
foldl f z t = appEndo (getDual (foldMap (Dual . Endo . flip f) t)) z
```

# dependencies
## 0
```haskell
appEndo :: Endo a -> a -> a
```
## 1
```haskell
getDual :: Dual a -> a
```
## 2
```haskell
foldMap :: Monoid m => (a -> m) -> t a -> m
```
## 3
```haskell
newtype Dual a = Dual { getDual :: a }
```
## 4
```haskell
newtype Endo a = Endo { appEndo :: a -> a }
```
## 5
```haskell
flip :: (a -> b -> c) -> b -> a -> c
```
## 6
```haskell
(.) :: (a -> a) -> (a -> a) -> (a -> a)
```
