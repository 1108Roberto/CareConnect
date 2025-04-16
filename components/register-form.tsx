"use client";

import type React from "react";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { toast } from "@/components/ui/use-toast";

export default function RegisterForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    cedula: "",
    password: "",
    nombre: "",
    apellido: "",
    fecha_de_nacimiento: "",
    email: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Error al registrar usuario");
      }

      toast({
        title: "Registro exitoso",
        description: "Su cuenta ha sido creada correctamente",
      });

      // Redirect to login page
      router.push("/");
    } catch (error) {
      console.error("Registration error:", error);
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Error al registrar usuario",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 w-32 h-32 relative">
          <Image
            src="/images/logo.png"
            alt="Logo"
            width={128}
            height={128}
            className="rounded-lg"
          />
        </div>
        <CardTitle className="text-2xl">Registro de Usuario</CardTitle>
        <CardDescription>
          Complete el formulario para crear su cuenta
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="nombre" className="text-sm font-medium">
              Nombre
            </label>
            <input
              id="nombre"
              name="nombre"
              type="text"
              value={formData.nombre}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              placeholder="Ingrese su nombre"
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="apellido" className="text-sm font-medium">
              Apellido
            </label>
            <input
              id="apellido"
              name="apellido"
              type="text"
              value={formData.apellido}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              placeholder="Ingrese su apellido"
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="cedula" className="text-sm font-medium">
              Cédula
            </label>
            <input
              id="cedula"
              name="cedula"
              type="text"
              value={formData.cedula}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              placeholder="Ingrese su número de cédula"
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium">
              Contraseña
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              placeholder="Ingrese su contraseña"
              required
            />
          </div>
          <div className="space-y-2">
            <label
              htmlFor="fecha_de_nacimiento"
              className="text-sm font-medium"
            >
              Fecha de Nacimiento
            </label>
            <input
              id="fecha_de_nacimiento"
              name="fecha_de_nacimiento"
              type="date"
              value={formData.fecha_de_nacimiento}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              placeholder="Ingrese su correo electrónico"
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Registrando..." : "Registrarse"}
          </Button>
        </form>
      </CardContent>
      <CardFooter className="flex flex-col space-y-2">
        <div className="text-center text-sm">
          ¿Ya tiene una cuenta?{" "}
          <Link href="/" className="text-blue-600 hover:underline">
            Iniciar Sesión
          </Link>
        </div>
      </CardFooter>
    </Card>
  );
}
