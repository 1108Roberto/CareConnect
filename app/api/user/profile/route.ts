import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { query } from "@/lib/db";
import { verify } from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET || "your-secret-key";

// Get user profile
export async function GET(request: Request) {
  try {
    // Get token from cookies
    const token = (await cookies()).get("auth_token")?.value;

    if (!token) {
      return NextResponse.json({ error: "No autorizado" }, { status: 401 });
    }

    // Verify token
    let decoded;
    try {
      decoded = verify(token, JWT_SECRET) as any;
    } catch (error) {
      return NextResponse.json({ error: "Token inválido" }, { status: 401 });
    }

    // Get user data from database
    const users = await query(
      "SELECT id, cedula, nombre, apellido, fecha_de_nacimiento, email FROM users WHERE id = ?",
      [decoded.id]
    );

    if (!Array.isArray(users) || users.length === 0) {
      return NextResponse.json(
        { error: "Usuario no encontrado" },
        { status: 404 }
      );
    }

    const user = users[0];

    return NextResponse.json({ user }, { status: 200 });
  } catch (error) {
    console.error("Error getting user profile:", error);
    return NextResponse.json(
      { error: "Error al obtener perfil de usuario" },
      { status: 500 }
    );
  }
}

// Update user profile
export async function PUT(request: Request) {
  try {
    // Get token from cookies
    const token = (await cookies()).get("auth_token")?.value;

    if (!token) {
      return NextResponse.json({ error: "No autorizado" }, { status: 401 });
    }

    // Verify token
    let decoded;
    try {
      decoded = verify(token, JWT_SECRET) as any;
    } catch (error) {
      return NextResponse.json({ error: "Token inválido" }, { status: 401 });
    }

    // Get request body
    const { nombre, apellido, email, fecha_de_nacimiento } =
      await request.json();

    // Validate required fields
    if (!nombre || !apellido || !email || !fecha_de_nacimiento) {
      return NextResponse.json(
        { error: "Todos los campos son requeridos" },
        { status: 400 }
      );
    }

    // Check if email is already in use by another user
    const existingUsers = await query(
      "SELECT * FROM users WHERE email = ? AND id != ?",
      [email, decoded.id]
    );

    if (Array.isArray(existingUsers) && existingUsers.length > 0) {
      return NextResponse.json(
        { error: "El email ya está en uso por otro usuario" },
        { status: 409 }
      );
    }

    // Update user data
    await query(
      "UPDATE users SET nombre = ?, apellido = ?, email = ?, fecha_de_nacimiento = ? WHERE id = ?",
      [nombre, apellido, email, fecha_de_nacimiento, decoded.id]
    );

    return NextResponse.json(
      { message: "Perfil actualizado exitosamente" },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error updating user profile:", error);
    return NextResponse.json(
      { error: "Error al actualizar perfil de usuario" },
      { status: 500 }
    );
  }
}
