
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--print

# poly_type
Ad-hoc

# signature
```haskell
print :: Show a => a -> IO ()
```   

# code
```haskell
print x =  putStrLn (show x)
```

# dependencies
## 0
```haskell
putStrLn :: String -> IO ()
```
## 1
```haskell
show :: Show a => a -> String
```
