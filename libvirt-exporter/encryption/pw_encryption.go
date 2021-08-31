package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
)

type AESCipher struct {
	block cipher.Block
}

func NewAesCipher(key []byte) (*AESCipher, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	return &AESCipher{block}, nil
}

func (a *AESCipher) EncryptString(s string) string {
	byteString := []byte(s)
	encryptByteArray := make([]byte, aes.BlockSize+len(s))

	iv := encryptByteArray[:aes.BlockSize]

	io.ReadFull(rand.Reader, iv)

	stream := cipher.NewCFBEncrypter(a.block, iv)
	stream.XORKeyStream(encryptByteArray[aes.BlockSize:], byteString)

	return base64.URLEncoding.EncodeToString(encryptByteArray)
}

func (a *AESCipher) DecryptString(base64String string) string {

	b, _ := base64.URLEncoding.DecodeString(base64String)
	byteString := []byte(b)

	decryptByteArray := make([]byte, len(byteString))
	iv := byteString[:aes.BlockSize]

	stream := cipher.NewCFBDecrypter(a.block, iv)
	stream.XORKeyStream(decryptByteArray, byteString[aes.BlockSize:])

	decPw := ""
	//byte 배열에 담긴 ascii 코드를 확인하여 32 (공백) 이상이면서 127(delete) 문자일 경우에 정상 문자로 인식
	for i, _ := range decryptByteArray {
		if decryptByteArray[i] > 31 && decryptByteArray[i] < 127 {
				decPw += string(decryptByteArray[i])
		}
	}

	return decPw
}

func main() {
	//키는 16, 24, 32만 가능합니다
	var key = []byte("ablestackwallkey")

	a, _ := NewAesCipher(key)
	e := a.EncryptString("Ablecloud1!")

	fmt.Println(e)

	//d := a.DecryptString(e)
	//fmt.Println(d)
	//fmt.Println(len(d))
}