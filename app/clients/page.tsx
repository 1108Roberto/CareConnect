import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function ClientsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Clients</h1>
        <Link href="/clients/new">
          <Button>Add New Client</Button>
        </Link>
      </div>

      <div className="bg-card rounded-lg shadow p-6">
        <p className="text-center text-muted-foreground">
          Client data will be loaded here from the database.
        </p>
      </div>
    </div>
  );
}
