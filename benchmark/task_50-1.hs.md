
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--mconcat-[]

# poly_type
Parametric

# signature
```haskell
mconcat :: [[a]] -> a
```   

# code
```haskell
mconcat xss = [x | xs <- xss, x <- xs]
```

# dependencies
