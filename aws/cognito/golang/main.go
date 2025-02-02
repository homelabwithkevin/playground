package main

import (
	"context"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"

	"github.com/coreos/go-oidc"
	"github.com/golang-jwt/jwt/v4"
	"github.com/joho/godotenv"
	"golang.org/x/oauth2"
)

type ClaimsPage struct {
	AccessToken string
	Claims      jwt.MapClaims
}

type UserInfo struct {
	Email         string `json:"email"`
	EmailVerified string `json:"email_verified"`
	Sub           string `json:"sub"`
	Username      string `json:"username"`
}

var (
	redirectURL  = "http://localhost:3000/callback"
	provider     *oidc.Provider
	oauth2Config oauth2.Config
)

func init() {
	var err error
	// Initialize DotEnv
	godotenv.Load()

	// Initialize OIDC provider
	provider, err = oidc.NewProvider(context.Background(), os.Getenv("issuerURL"))
	if err != nil {
		log.Fatalf("Failed to create OIDC provider: %v", err)
	}

	// Set up OAuth2 config
	oauth2Config = oauth2.Config{
		ClientID:    os.Getenv("clientId"),
		RedirectURL: redirectURL,
		Endpoint:    provider.Endpoint(),
		Scopes:      []string{oidc.ScopeOpenID, "email", "openid"},
	}
}

func main() {
	http.HandleFunc("/", handleHome)
	http.HandleFunc("/login", handleLogin)
	http.HandleFunc("/logout", handleLogout)
	http.HandleFunc("/callback", handleCallback)
	http.HandleFunc("/userInfo", handleUserInfo)

	fmt.Println("Server is running on http://localhost:3000")
	log.Fatal(http.ListenAndServe(":3000", nil))
}

func handleHome(w http.ResponseWriter, r *http.Request) {
	html := `
        <html>
        <body>
            <h1>Welcome to Cognito OIDC Go App</h1>
            <a href="/login">Login with Cognito</a>
        </body>
        </html>`
	fmt.Fprint(w, html)
}

func handleLogin(writer http.ResponseWriter, request *http.Request) {
	state := "state" // Replace with a secure random string in production
	url := oauth2Config.AuthCodeURL(state, oauth2.AccessTypeOffline)
	http.Redirect(writer, request, url, http.StatusFound)
}

func handleCallback(writer http.ResponseWriter, request *http.Request) {
	ctx := context.Background()
	code := request.URL.Query().Get("code")

	// Exchange the authorization code for a token
	rawToken, err := oauth2Config.Exchange(ctx, code)
	if err != nil {
		http.Error(writer, "Failed to exchange token: "+err.Error(), http.StatusInternalServerError)
		return
	}
	tokenString := rawToken.AccessToken

	// Parse the token (do signature verification for your use case in production)
	token, _, err := new(jwt.Parser).ParseUnverified(tokenString, jwt.MapClaims{})
	if err != nil {
		fmt.Printf("Error parsing token: %v\n", err)
		return
	}

	// Check if the token is valid and extract claims
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		http.Error(writer, "Invalid claims", http.StatusBadRequest)
		return
	}

	// Prepare data for rendering the template
	pageData := ClaimsPage{
		AccessToken: tokenString,
		Claims:      claims,
	}

	// Define the HTML template
	tmpl := `
    <html>
        <body>
            <h1>User Information</h1>
            <h1>JWT Claims</h1>
            <p><strong>Access Token:</strong> {{.AccessToken}}</p>
            <ul>
                {{range $key, $value := .Claims}}
                    <li><strong>{{$key}}:</strong> {{$value}}</li>
                {{end}}
            </ul>
            <a href="/userInfo?accessToken={{.AccessToken}}">User Info</a>
            <a href="/logout">Logout</a>
        </body>
    </html>`

	// Parse and execute the template
	t := template.Must(template.New("claims").Parse(tmpl))
	t.Execute(writer, pageData)
}

func handleUserInfo(writer http.ResponseWriter, request *http.Request) {
	userPoolDomain := os.Getenv("userPoolDomain")
	url := userPoolDomain + "/oauth2/userInfo"
	accessToken := request.URL.Query().Get("accessToken")

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatalf("Error: %s", err)
	}

	req.Header.Set("Authorization", "Bearer "+accessToken)

	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		panic(err)
	}

	defer resp.Body.Close()

	var j UserInfo

	err = json.NewDecoder(resp.Body).Decode(&j)

	if err != nil {
		panic(err)
	}

	// Define the HTML template
	tmpl := `
    <html>
        <body>
            <h1>User Information</h1>
            <ul>
				<p>{{.Email}}</p>
            </ul>
            <a href="/logout">Logout</a>
        </body>
    </html>`

	// Parse and execute the template
	t := template.Must(template.New("userinfo").Parse(tmpl))
	t.Execute(writer, j)
}

func handleLogout(writer http.ResponseWriter, request *http.Request) {
	// Here, you would clear the session or cookie if stored.
	http.Redirect(writer, request, "/", http.StatusFound)
}
