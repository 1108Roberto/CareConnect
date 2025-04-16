import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { verify } from "jsonwebtoken"

const JWT_SECRET = process.env.JWT_SECRET || "your-secret-key"

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname

  // Define public paths that don't require authentication
  const isPublicPath = path === "/" || path === "/registro" || path.startsWith("/api/auth")

  // Get the token from the cookies
  const token = request.cookies.get("auth_token")?.value

  // If the path requires authentication and there's no token, redirect to login
  if (!isPublicPath && !token) {
    return NextResponse.redirect(new URL("/", request.url))
  }

  // If the user is logged in and trying to access login/register pages, redirect to dashboard
  if (isPublicPath && token && (path === "/" || path === "/registro")) {
    try {
      // Verify the token
      verify(token, JWT_SECRET)
      return NextResponse.redirect(new URL("/dashboard", request.url))
    } catch (error) {
      // If token verification fails, clear the cookie and continue
      const response = NextResponse.next()
      response.cookies.delete("auth_token")
      return response
    }
  }

  return NextResponse.next()
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/auth/logout).*)"],
}
