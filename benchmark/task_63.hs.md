
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--product

# poly_type
Ad-hoc

# signature
```haskell
product :: (Foldable t, Num a) => t a -> a
```   

# code
```haskell
product = getProduct #. foldMap' Product
```

# dependencies
## 0
```haskell
getProduct :: Product a -> a
```
## 1
```haskell
(#.) :: Coercible b c => (b -> c) -> (a -> b) -> (a -> c)
```
## 2
```haskell
foldMap' :: Monoid m => (a -> m) -> t a -> m
```
## 3
```haskell
newtype Product a = Product {getProduct :: a}
```
