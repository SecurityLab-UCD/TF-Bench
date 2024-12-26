
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--scanr

# poly_type
Parametric

# signature
```haskell
scanr :: (a -> b -> b) -> b -> [a] -> [b]
```   

# code
```haskell
scanr _ q0 []           =  [q0]
scanr f q0 (x:xs)       =  f x q : qs
                           where qs@(q:_) = scanr f q0 xs
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```