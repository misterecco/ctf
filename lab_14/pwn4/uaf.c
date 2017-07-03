#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// gcc uaf.c -o uaf

struct Product {
	char name[24];
	unsigned int amount;
};

struct ShoppingListElement {
	void (*buy_routine)(struct Product*, unsigned int index);
	struct Product* product;
	char bought;
};

struct Product * products[8];
struct ShoppingListElement * shopping_list[8];

unsigned int products_amount;
unsigned int shopping_list_amount;

void add_product()
{	
	struct Product* product;
	unsigned int name_length;
	
	if(products_amount >= 8)
	{
		printf("You cannot add more products!\n");
		return;
	}
	
	product = malloc(sizeof(struct Product));
	
	do {
		printf("Length of product name:\n");
		scanf("%u", &name_length);
		fgetc(stdin);
	} while(name_length >= 24);

	printf("Product name:\n");
	read(0, product->name, name_length);
	fgetc(stdin);

	printf("Product amount:\n");
	scanf("%u", &(product->amount));
	fgetc(stdin);
	
	products[products_amount++] = product;
}

void list_products()
{
	printf("Products:\n\n");
	for(int i=0; i<products_amount; i++)
		printf("%d. %u %s\n", i, products[i]->amount, products[i]->name);
	printf("-----------\n");
}

void buy_product(struct Product* product, unsigned int index)
{
	printf("Bought %u of %s (%u)\n", product->amount, 
	                                 product->name,
	                                 index);
}

void add_to_shopping_list()
{
	struct ShoppingListElement* element;
	unsigned int product_id;
	
	if(shopping_list_amount >= 8)
	{
		printf("You cannot add more entries to shopping list!\n");
		return;
	}

	list_products();
	
	printf("Product id:\n");
	scanf("%u", &product_id);
	fgetc(stdin);
	
	if(product_id >= products_amount)
	{
		printf("This product doesn't exist!\n");
		return;
	}
	
	element = malloc(sizeof(struct ShoppingListElement));
	element->buy_routine = buy_product;
	element->product = products[product_id];
	element->bought = 0;
	
	shopping_list[shopping_list_amount++] = element;
}

void list_elements()
{
	struct Product* product;
	printf("Shopping list:\n\n");
	for(int i=0; i<shopping_list_amount; i++)
	{
		if(shopping_list[i]->bought)
		{
			printf("%d. ---bought---\n", i);
		} else
		{
			product = shopping_list[i]->product;
			printf("%d. %u %s\n", i, product->amount, product->name);
		}
	}
	printf("-----------\n");
}


void buy_from_shopping_list()
{
	struct ShoppingListElement* element;
	unsigned int element_id;
	printf("Which product you wish to buy:\n");
	scanf("%u", &element_id);
	fgetc(stdin);
	
	if(!shopping_list[element_id])
	{
		printf("This element doesn't exist!\n");
		return;
	}
	
	element = shopping_list[element_id];
	element->buy_routine(element->product, element_id);
	element->bought = 1;
	
	free(shopping_list[element_id]);
}

int main()
{
	char cmd;
	do
	{
		printf("1. Add product\n");
		printf("2. Add to shopping list\n");
		printf("3. Buy from shopping list\n");
		printf("4. List shopping list\n");
		printf("0. Exit\n");
		
		scanf("%c", &cmd);
		fgetc(stdin);
		printf("-----------\n");
		switch(cmd)
		{
			case '1':
				add_product();
				break;
			case '2':
				add_to_shopping_list();
				break;
			case '3':
				buy_from_shopping_list();
				break;
			case '4':
				list_elements();
				break;
		}
	} while(cmd != '0');
	return 0;
}
