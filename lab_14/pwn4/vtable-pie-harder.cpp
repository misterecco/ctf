#include <vector>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <unistd.h>

// g++ -pie -fPIC vtable.cpp -o vtable

void getarg(char* buf, unsigned n)
{
	fgets(buf, n, stdin);
	buf[strcspn(buf, "\n")] = '\0';
}

void getargl(char* buf, unsigned max)
{
	unsigned n;
	printf("Length:\n");
	scanf("%d", &n);
	fgetc(stdin);
	if(n > max)
	{
		printf("No no no.. it's too long!\n");
		return;
	}
	printf("Say:\n");
	read(0, buf, n);
	fgetc(stdin);
}

struct Object
{
	char buf[32];
	
	Object(const char* _buf)
	{
		strcpy(buf, _buf);
	}
	
	virtual void execute() = 0;
	
	virtual void modify() = 0;
};

struct PrintObject: Object
{
	PrintObject(const char* _buf): Object(_buf) { }
	
	virtual void execute()
	{
		printf("%s\n", buf);
	}
	
	virtual void modify()
	{
		getargl(buf, 41);
	}
};

struct CommandObject: Object
{
	CommandObject(): Object("ls") {}
	
	virtual void execute()
	{
		system(buf);
	}

	virtual void modify()
	{
		printf("You can't modify CommandObject!\n");
	}
};

std::vector<Object*> objects;

int main()
{
	char buf[256];
	
	objects.reserve(32);
	
	while(1)
	{
		Object * obj;
		printf("Command:\n");
		getarg(buf, 256);
		if(!strcmp(buf, "print"))
		{
			printf("Say:\n");
			getarg(buf, 256);
			obj = new PrintObject(buf);
			objects.push_back(obj);
		} else if(!strcmp(buf, "command"))
		{
			obj = new CommandObject();
			objects.push_back(obj);
		} else if(!strcmp(buf, "do"))
		{
			for(std::vector<Object*>::iterator it = objects.begin(); it != objects.end(); ++it)
				(*it)->execute();
		} else if(!strcmp(buf, "edit"))
		{
			unsigned int id;
			printf("Object id:\n");
			scanf("%u", &id);
			fgetc(stdin);
			
			if(id >= objects.size())
			{
				printf("Object not found!\n");
			} else
			{
				objects[id]->modify();
			}
		
		} else if(!strcmp(buf, "exit"))
		{
			exit(0);
		}
	}
}
