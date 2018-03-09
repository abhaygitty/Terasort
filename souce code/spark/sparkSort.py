
public class BinarySearchTree {
	
	int[] array = {0,1,2,3,4};
	int mid, 
	high = array.length-1, 
	low = 0;
	
	
	public void binaryTree(int searchValue){
		while(low<=high && array[mid]!=searchValue){
			if(array[mid] > searchValue)
				//shift high to mid-1
				high = mid-1;
			else //searchvalue is on the second half of the array do shift the low beyond the midpoint
				low = mid+1;
			
			mid = (high + low)/2;
		}
		
		if(low > high)
			//not found
			System.out.println("Not found!");
		else 
			System.out.println(mid + " found");
		
	}
	

}
