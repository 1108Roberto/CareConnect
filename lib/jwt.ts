import { verify } from "jsonwebtoken";
import type { JWTPayload } from "@/types";

const JWT_SECRET = process.env.JWT_SECRET || "";

export function verifyToken(token: string): JWTPayload | null {
  try {
    return verify(token, JWT_SECRET) as JWTPayload;
  } catch (error) {
    console.error("Token verification error:", error);
    return null;
  }
}
