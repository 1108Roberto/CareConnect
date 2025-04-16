import { NextResponse } from "next/server";
import { query } from "@/lib/db";
import { generateToken } from "@/lib/utils";

export async function POST(request: Request) {
  try {
    const { cedula } = await request.json();

    if (!cedula) {
      return NextResponse.json(
        { error: "La cédula es requerida" },
        { status: 400 }
      );
    }

    // Check if user exists
    const users = await query("SELECT * FROM users WHERE cedula = ?", [cedula]);

    if (!Array.isArray(users) || users.length === 0) {
      return NextResponse.json(
        { error: "Usuario no encontrado" },
        { status: 404 }
      );
    }

    // Generate reset token
    const resetToken = generateToken(32);
    const resetExpires = new Date(Date.now() + 3600000); // 1 hour from now

    // Store reset token in database
    await query(
      "UPDATE users SET reset_token = ?, reset_expires = ? WHERE cedula = ?",
      [resetToken, resetExpires, cedula]
    );

    // In a real application, you would send an email with the reset token
    // Since we're running locally, we'll just return the token in the response
    // for testing purposes

    return NextResponse.json(
      {
        message: "Token de restablecimiento generado",
        resetToken: resetToken, // Only for local testing
      },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error requesting password reset:", error);
    return NextResponse.json(
      { error: "Error al solicitar restablecimiento de contraseña" },
      { status: 500 }
    );
  }
}
