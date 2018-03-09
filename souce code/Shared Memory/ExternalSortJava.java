package Sorts.SelectionSort;

public class SelectionSortApp {

	public static void main(String[] args) 
	{
		SelectionArray sArr = new SelectionArray(20,true);
		for(int i=0; i<20; i++)
		{
			sArr.insertElement(0+(int)(Math.random()*100));
		}
		
		//sArr.displayElems();
		sArr.selectionSort();
		sArr.displayElems();
	}

}
