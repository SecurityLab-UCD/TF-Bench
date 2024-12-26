
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--head

# poly_type
Polymorphic

# note
modified

# signature
```haskell
head :: [a] -> a
```   

# code
```haskell
head (x:_)              =  x
head []                 =  error "empty"
```

# dependencies
## 1
```haskell
(:) :: a -> [a] -> [a]
```