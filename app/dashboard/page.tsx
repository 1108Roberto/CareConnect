import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Button variant="outline" asChild>
          <Link href="/api/auth/logout">Cerrar Sesión</Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Bienvenido</h2>
          <p className="text-gray-600 dark:text-gray-300">
            Has iniciado sesión correctamente en el sistema.
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Perfil de Usuario</h2>
          <p className="text-gray-600 dark:text-gray-300">
            Aquí podrás ver y editar tu información personal.
          </p>
          <Button className="mt-4" variant="outline" asChild>
            <Link href="/profile">Ver Perfil</Link>
          </Button>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Configuración</h2>
          <p className="text-gray-600 dark:text-gray-300">
            Ajusta las preferencias de tu cuenta.
          </p>
          <Button className="mt-4" variant="outline" asChild>
            <Link href="/settings">Configurar</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
