
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--writeFile

# poly_type
Monomorphic

# signature
```haskell
writeFile :: FilePath -> String -> IO ()
```   

# code
```haskell
writeFile f txt = withFile f WriteMode (\ hdl -> hPutStr hdl txt)
```

# dependencies
## 0
```haskell
hPutStr :: Handle -> String -> IO ()
```
## 1
```haskell
withFile :: FilePath -> IOMode -> (Handle -> IO r) -> IO r
```
## 2
```haskell
data IOMode = ReadMode | WriteMode | AppendMode | ReadWriteMode
```