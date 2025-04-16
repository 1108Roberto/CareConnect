import { NextResponse } from "next/server";
import { query } from "@/lib/db";
import bcrypt from "bcrypt";

export async function POST(request: Request) {
  try {
    const { cedula, token, password } = await request.json();

    if (!cedula || !token || !password) {
      return NextResponse.json(
        { error: "Todos los campos son requeridos" },
        { status: 400 }
      );
    }

    // Check if user exists and token is valid
    const users = await query(
      "SELECT * FROM users WHERE cedula = ? AND reset_token = ? AND reset_expires > NOW()",
      [cedula, token]
    );

    if (!Array.isArray(users) || users.length === 0) {
      return NextResponse.json(
        { error: "Token inválido o expirado" },
        { status: 400 }
      );
    }

    // Hash new password
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Update password and clear reset token
    await query(
      "UPDATE users SET password = ?, reset_token = NULL, reset_expires = NULL WHERE cedula = ?",
      [hashedPassword, cedula]
    );

    return NextResponse.json(
      { message: "Contraseña restablecida exitosamente" },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error resetting password:", error);
    return NextResponse.json(
      { error: "Error al restablecer contraseña" },
      { status: 500 }
    );
  }
}
